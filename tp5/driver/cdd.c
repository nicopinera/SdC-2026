// cdd.c — Character Device Driver para Raspberry Pi
//
// Crea /dev/cdd con dos operaciones:
//   read  → devuelve el valor actual de la señal activa (ASCII + '\n')
//   write → cambia la señal activa ("1" o "2")
//
// Un kernel timer actualiza el valor cada 1 segundo.
//   Señal 1: temperatura simulada, 20–35 °C
//   Señal 2: presión simulada, 950–1050 hPa

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/device.h>
#include <linux/uaccess.h>
#include <linux/timer.h>
#include <linux/random.h>
#include <linux/jiffies.h>
#include <linux/spinlock.h>

#define DEVICE_NAME "cdd"
#define CLASS_NAME  "cdd"

static dev_t          dev_num;
static struct cdev    cdd_cdev;
static struct class  *cdd_class;
static struct device *cdd_dev;

static int active_signal = 1;
static int current_value = 0;
static DEFINE_SPINLOCK(cdd_lock);

static struct timer_list update_timer;

// Genera un nuevo valor segun la señal activa y reprograma el timer.
static void update_value(struct timer_list *t)
{
    unsigned int rnd;
    int val;

    get_random_bytes(&rnd, sizeof(rnd));

    spin_lock(&cdd_lock);
    if (active_signal == 1)
        val = 20 + (int)(rnd % 16);     // 20–35 °C
    else
        val = 950 + (int)(rnd % 101);   // 950–1050 hPa
    current_value = val;
    spin_unlock(&cdd_lock);

    mod_timer(&update_timer, jiffies + HZ);
}

static int cdd_open(struct inode *inode, struct file *file)
{
    return 0;
}

static int cdd_release(struct inode *inode, struct file *file)
{
    return 0;
}

// Retorna el valor actual como string ASCII. Cada open() parte desde offset 0,
// por lo que la app de usuario puede leer reabriendo el dispositivo cada vez.
static ssize_t cdd_read(struct file *file, char __user *buf, size_t len, loff_t *off)
{
    char tmp[16];
    int  n, val;

    if (*off > 0)
        return 0;   // EOF — ya se envió el dato en este open()

    spin_lock(&cdd_lock);
    val = current_value;
    spin_unlock(&cdd_lock);

    n = snprintf(tmp, sizeof(tmp), "%d\n", val);
    if ((size_t)n > len)
        return -EINVAL;
    if (copy_to_user(buf, tmp, n))
        return -EFAULT;

    *off += n;
    return n;
}

// Recibe "1" o "2" (con o sin '\n') y actualiza la señal activa.
static ssize_t cdd_write(struct file *file, const char __user *buf, size_t len, loff_t *off)
{
    char tmp[8];
    int  sig;
    size_t trim;

    if (len == 0 || len >= sizeof(tmp))
        return -EINVAL;
    if (copy_from_user(tmp, buf, len))
        return -EFAULT;

    tmp[len] = '\0';
    trim = len;
    while (trim > 0 && (tmp[trim - 1] == '\n' || tmp[trim - 1] == '\r' || tmp[trim - 1] == ' '))
        tmp[--trim] = '\0';

    if (kstrtoint(tmp, 10, &sig))
        return -EINVAL;
    if (sig != 1 && sig != 2)
        return -EINVAL;

    spin_lock(&cdd_lock);
    active_signal = sig;
    spin_unlock(&cdd_lock);

    return (ssize_t)len;
}

static const struct file_operations cdd_fops = {
    .owner   = THIS_MODULE,
    .open    = cdd_open,
    .release = cdd_release,
    .read    = cdd_read,
    .write   = cdd_write,
};

static int __init cdd_init(void)
{
    int ret;

    ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
    if (ret < 0) {
        pr_err("cdd: alloc_chrdev_region fallo (%d)\n", ret);
        return ret;
    }

    cdev_init(&cdd_cdev, &cdd_fops);
    ret = cdev_add(&cdd_cdev, dev_num, 1);
    if (ret < 0) {
        pr_err("cdd: cdev_add fallo (%d)\n", ret);
        goto err_chrdev;
    }

    cdd_class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(cdd_class)) {
        ret = PTR_ERR(cdd_class);
        pr_err("cdd: class_create fallo (%d)\n", ret);
        goto err_cdev;
    }

    cdd_dev = device_create(cdd_class, NULL, dev_num, NULL, DEVICE_NAME);
    if (IS_ERR(cdd_dev)) {
        ret = PTR_ERR(cdd_dev);
        pr_err("cdd: device_create fallo (%d)\n", ret);
        goto err_class;
    }

    timer_setup(&update_timer, update_value, 0);
    mod_timer(&update_timer, jiffies + HZ);

    pr_info("cdd: cargado — /dev/%s (major=%d)\n", DEVICE_NAME, MAJOR(dev_num));
    return 0;

err_class:
    class_destroy(cdd_class);
err_cdev:
    cdev_del(&cdd_cdev);
err_chrdev:
    unregister_chrdev_region(dev_num, 1);
    return ret;
}

static void __exit cdd_exit(void)
{
    del_timer_sync(&update_timer);
    device_destroy(cdd_class, dev_num);
    cdev_del(&cdd_cdev);
    class_destroy(cdd_class);
    unregister_chrdev_region(dev_num, 1);
    pr_info("cdd: descargado\n");
}

module_init(cdd_init);
module_exit(cdd_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Bare metal guys");
MODULE_DESCRIPTION("CDD — simulador de seniales para Raspberry Pi");
MODULE_VERSION("1.0");
