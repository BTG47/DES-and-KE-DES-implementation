# Contexto técnico para OpenCode: DES y KE-DES

Hola. Vas a continuar un proyecto académico de **Seguridad Informática** cuyo objetivo es implementar y comparar **DES** y una variante propuesta llamada **KE-DES (Key-Based Enhancement of DES)**.

El trabajo ya tiene una implementación propia en Python construida manualmente por el estudiante. La prioridad es **conservar esa implementación**, corregir únicamente lo necesario y evitar sobreingeniería. Menos código es mejor si mantiene claridad, corrección y trazabilidad con el algoritmo.

No reemplaces la implementación por bibliotecas criptográficas externas ni por wrappers de OpenSSL, PyCryptodome, `cryptography`, etc. La tarea exige una implementación propia.

---

# 1. DES — Resumen técnico

## Objetivo

DES es un cifrador simétrico por bloques con:

- bloque de entrada: **64 bits**
- clave de entrada: **64 bits**
- clave efectiva: **56 bits**
- estructura: **Feistel**
- rondas: **16**

La implementación actual ya reproduce correctamente el vector clásico:

```text
Plaintext:  0123456789ABCDEF
Key:        133457799BBCDFF1
Ciphertext: 85E813540F0AB405
```

El descifrado también recupera correctamente el plaintext usando las subclaves en orden inverso.

---

## 1.1 Flujo general de DES

```text
Plaintext 64 bits
        |
        v
Initial Permutation (IP)
        |
        v
+-----------------------+
| L0 (32) | R0 (32)     |
+-----------------------+
        |
        v
16 rondas Feistel
        |
        v
+-----------------------+
| L16     | R16         |
+-----------------------+
        |
        v
Swap final: R16 || L16
        |
        v
Inverse Initial Permutation (IP^-1)
        |
        v
Ciphertext 64 bits
```

---

## 1.2 Estructura Feistel

Cada ronda usa:

```text
Li = Ri-1
Ri = Li-1 XOR F(Ri-1, Ki)
```

donde:

- `Li`, `Ri`: mitades izquierda y derecha
- `Ki`: subclave de la ronda
- `F`: función interna de DES

La gran ventaja práctica es que el descifrado usa la misma estructura, invirtiendo únicamente el orden de las subclaves.

---

## 1.3 Generación de subclaves DES

### Paso 1 — PC-1

La clave original de 64 bits pasa por **Permuted Choice 1 (PC-1)**.

Resultado:

```text
64 bits -> PC-1 -> 56 bits
```

Los 8 bits descartados corresponden a posiciones de paridad.

### Paso 2 — División

Los 56 bits se dividen:

```text
C0 = 28 bits
D0 = 28 bits
```

### Paso 3 — Rotaciones

Cada ronda aplica una rotación circular izquierda a `C` y `D`.

Calendario:

```text
1, 1, 2, 2,
2, 2, 2, 2,
1, 2, 2, 2,
2, 2, 2, 1
```

### Paso 4 — PC-2

Después de cada rotación:

```text
Cn || Dn -> PC-2 -> Kn
```

La salida de PC-2 tiene 48 bits.

Se generan:

```text
K1, K2, ..., K16
```

---

## 1.4 Función F de DES

La función `F` toma:

- `R`: 32 bits
- `K`: 48 bits

Flujo:

```text
R(32)
 |
 v
Expansion E
 |
 v
48 bits
 |
 XOR K
 |
 v
48 bits
 |
 v
8 S-Boxes
 |
 v
32 bits
 |
 v
Permutation P
 |
 v
F(R,K) = 32 bits
```

### Expansion E

Expande 32 bits a 48 bits repitiendo determinadas posiciones.

### XOR

```text
E(R) XOR Ki
```

### S-Boxes

Los 48 bits se dividen en 8 bloques de 6 bits.

Cada bloque entra a una S-Box:

```text
6 bits -> S-Box -> 4 bits
```

Para cada bloque:

```text
fila    = primer bit + último bit
columna = cuatro bits centrales
```

Las 8 S-Boxes producen:

```text
8 x 4 = 32 bits
```

### Permutation P

Los 32 bits se reorganizan mediante la tabla `P`.

---

## 1.5 Descifrado DES

El algoritmo estructural es el mismo.

Única diferencia:

```text
Cifrado:
K1, K2, ..., K16

Descifrado:
K16, K15, ..., K1
```

Por eso la implementación puede reutilizar el mismo `des_process()`.

---

# 2. KE-DES — Resumen técnico

## Objetivo

KE-DES es una variante académica propuesta en el artículo:

**O. Reyad, H. M. Mansour, M. Heshmat, E. A. Zanaty, "Key-Based Enhancement of Data Encryption Standard for Text Security", 2021.**

La tarea académica indica explícitamente que **KE-DES no debe considerarse criptográficamente seguro**. Su objetivo aquí es estudiar una variante de DES y comparar sus operaciones.

KE-DES conserva gran parte de DES y modifica principalmente:

1. la generación de claves mediante una transformación **Odd/Even**
2. la expansión estándar `E` mediante una nueva función **K-D (Key-Distribution)**

---

# 3. Qué se conserva entre DES y KE-DES

Se reutilizan:

- bloque de 64 bits
- clave de entrada de 64 bits
- IP
- IP^-1
- estructura Feistel
- 16 rondas
- S-Boxes
- permutación P
- XOR
- swap final
- lógica general de cifrado y descifrado

Por ello, KE-DES debe construirse como una **modificación mínima** sobre DES, no como una reimplementación completa.

---

# 4. Cambio 1 — Generación de claves KE-DES

El paper parte de una clave de 64 bits y aplica PC-1.

```text
64-bit key
   |
   v
PC-1
   |
   v
56 bits
```

Luego introduce una transformación llamada **Odd/Even**.

---

## 4.1 Odd/Even

El pseudocódigo del artículo indica:

```text
for j = 1 to size(B):
    if j mod 2 == 0:
        B[j] = 1
    else:
        B[j] = 0
```

Es importante:

- la condición depende de la **posición**
- no depende del valor actual del bit

Por ejemplo, sobre 56 posiciones se genera un patrón alternado.

El ejemplo del paper muestra:

```text
Odd/Even result:
01010101 01010101 01010101 01010101
01010101 01010101 01010101
```

y después se divide en:

```text
C0 = 0101010101010101010101010101
D0 = 1010101010101010101010101010
```

---

## 4.2 Ambigüedad importante del paper

Existe una inconsistencia entre:

- el texto del procedimiento
- la Figura 4
- los valores publicados en las tablas de resultados

El texto dice que los pasos 2 a 6 se repiten para generar K2...K16, lo que puede interpretarse como volver a aplicar Odd/Even cada ronda.

Sin embargo, los valores publicados de `C0`, `D0`, `C1`, `D1`, `K1`, `K2`, etc. deben ser usados como referencia al depurar la implementación.

No asumir silenciosamente una interpretación. El agente debe:

1. reproducir los valores del paper cuando sea posible
2. documentar cualquier contradicción encontrada
3. conservar una interpretación explícita en comentarios/tests

Valores de referencia del paper para la clave:

```text
133457799BBCDFF1
```

Subclaves publicadas:

```text
K1 =
011011101010110000011010010000110001100110111101

K2 =
100100010101001111100101101111001110011001000010
```

Estos valores deben servir como checkpoints de validación.

---

# 5. Cambio 2 — Función K-D

DES usa:

```text
R(32) -> Expansion E -> 48 bits
```

KE-DES reemplaza esa expansión por una construcción de 48 bits llamada **K-D**.

Según el paper:

```text
8 bits asociados a PC-1
+
32 bits de R
+
8 bits asociados a PC-2
=
48 bits
```

Por tanto:

```text
K-D = PC1_KD(8) || R(32) || PC2_KD(8)
```

Después de construir estos 48 bits, el resto de `F` se conserva:

```text
K-D output
    |
 XOR round key
    |
 S-Boxes
    |
 P
    |
32 bits
```

---

## 5.1 Selección PC1 para K-D

La Figura 1 del paper muestra:

```text
8, 16, 24, 32, 40, 48, 56, 64
```

La interpretación utilizada actualmente es:

```python
PC1_KD_SELECTION = [
    8, 16, 24, 32, 40, 48, 56, 64
]
```

aplicada sobre la **clave original de 64 bits**.

Esto se hace porque el texto del paper es ambiguo: llama a estos bits "PC-1 outcome", pero la posición 64 no puede existir en una salida de PC-1 de 56 bits.

Esta ambigüedad debe mantenerse documentada.

---

## 5.2 Selección PC2 para K-D

La Figura 1 muestra:

```text
9, 18, 27, 36, 15, 22, 29, 4
```

La implementación actual usa:

```python
PC2_KD_SELECTION = [
    9, 18, 27, 36, 15, 22, 29, 4
]
```

aplicada sobre la salida PC-2 de la ronda.

Esto produce 8 bits.

Los bits PC2 K-D cambian por ronda.

---

# 6. Flujo completo KE-DES por ronda

Conceptualmente:

```text
Ln, Rn
   |
   |-----------------------------+
   |                             |
   |                         Rn = 32 bits
   |                             |
   |               +-------------+-------------+
   |               |                           |
   |          PC1 KD bits                   PC2 KD bits
   |             8 bits                       8 bits
   |               |                           |
   |               +------ K-D = 48 bits ------+
   |                             |
   |                       XOR round key
   |                             |
   |                          S-Boxes
   |                             |
   |                             P
   |                             |
   +------------ XOR ------------+
                 |
                 v
              R(n+1)

L(n+1) = Rn
```

---

# 7. Descifrado KE-DES

La estructura Feistel sigue siendo reutilizable.

Para descifrar:

- invertir las subclaves
- invertir también las selecciones PC2 K-D correspondientes a cada ronda
- mantener PC1 K-D constante

Ejemplo conceptual:

```text
Encryption:
K1 + PC2_1
K2 + PC2_2
...
K16 + PC2_16

Decryption:
K16 + PC2_16
K15 + PC2_15
...
K1 + PC2_1
```

La implementación actual ya logra recuperar:

```text
0123456789ABCDEF
```

después de cifrar y descifrar con KE-DES.

Sin embargo, un round-trip correcto no es suficiente para confirmar que la implementación reproduce exactamente el paper; por eso los valores internos publicados deben usarse como validación adicional.

---

# 8. Estado actual del código

La implementación está dividida principalmente en:

```text
utilities.py
key_generator.py
function_F.py
des.py
```

Funciones importantes ya existentes:

```text
permute()
xor()
left_shift_array()

key_generation()
ke_des_generation()

function_F()

des_round()
des_process()

k_des_round()
k_des_process()
```

La arquitectura actual tiene una idea correcta que debe conservarse:

```text
DES:
R -> expansion_des() -> function_F()

KE-DES:
R -> expansion_kd() -> function_F()
```

`function_F()` recibe ya los 48 bits preparados y por tanto puede reutilizarse en ambos algoritmos.

---

# 9. Restricciones para continuar el proyecto

## Conservar

- la implementación manual existente
- las tablas DES
- la estructura de archivos actual si no existe una razón fuerte para cambiarla
- `permute`
- `xor`
- `function_F`
- generación manual de claves
- estructura Feistel
- estilo simple del proyecto

## Evitar

- reescribir todo desde cero
- clases innecesarias
- patrones de diseño
- abstracciones complejas
- librerías criptográficas externas
- duplicación de lógica
- cambios grandes que no sean necesarios para corregir el algoritmo
- añadir infraestructura no requerida

Principio de diseño:

> **Menos es más. Corregir y completar, no reinventar.**

---

# 10. Validaciones conocidas

## DES

Para:

```text
Plaintext:
0123456789ABCDEF

Key:
133457799BBCDFF1
```

resultado esperado:

```text
Ciphertext:
85E813540F0AB405
```

y:

```text
decrypt(ciphertext) =
0123456789ABCDEF
```

---

## KE-DES

Debe cumplir como mínimo:

```text
decrypt(encrypt(M, K), K) == M
```

y se deben contrastar las subclaves con los resultados publicados:

```text
K1 =
011011101010110000011010010000110001100110111101

K2 =
100100010101001111100101101111001110011001000010
```

Si estos valores no coinciden, diagnosticar primero la generación KE-DES antes de modificar el resto del algoritmo.

---

# 11. Objetivo inmediato para el agente

Antes de cualquier interfaz, refactor o limpieza:

1. leer y comprender la implementación existente
2. ejecutar los tests actuales
3. confirmar que DES sigue correcto
4. localizar el problema exacto en la generación KE-DES
5. contrastar cada etapa con los valores del paper
6. hacer la corrección mínima necesaria
7. conservar la mayor cantidad posible del código original

No continuar con mejoras secundarias hasta que el núcleo de KE-DES quede validado.

