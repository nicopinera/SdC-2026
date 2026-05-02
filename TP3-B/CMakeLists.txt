cmake_minimum_required(VERSION 3.16)
project(uefi_app C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_library(uefi_obj OBJECT src/aplicacion.c)

target_include_directories(
  uefi_obj PRIVATE /usr/include/efi /usr/include/efi/x86_64
                   /usr/include/efi/protocol)

target_compile_options(
  uefi_obj PRIVATE -fpic -ffreestanding -fno-stack-protector
                   -fno-strict-aliasing -fshort-wchar -mno-red-zone)

add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/uefi_program.so
  COMMAND
    ld -shared -Bsymbolic -nostdlib -znocombreloc -T /usr/lib/elf_x86_64_efi.lds
    /usr/lib/crt0-efi-x86_64.o $<TARGET_OBJECTS:uefi_obj> -L /usr/lib -L
    /usr/lib/efi -lefi -lgnuefi -o ${CMAKE_CURRENT_BINARY_DIR}/uefi_program.so
  DEPENDS uefi_obj
  VERBATIM)

# objcopy a .efi
add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/uefi_program.efi
  COMMAND
    objcopy -j .text -j .sdata -j .data -j .dynamic -j .dynsym -j .rel -j .rela
    -j .rel.* -j .rela.* -j .reloc --target=efi-app-x86_64
    ${CMAKE_CURRENT_BINARY_DIR}/uefi_program.so
    ${CMAKE_CURRENT_BINARY_DIR}/uefi_program.efi
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/uefi_program.so
  VERBATIM)

add_custom_target(uefi_program ALL
                  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/uefi_program.efi)
