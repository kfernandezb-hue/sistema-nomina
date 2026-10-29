# Sistema de Nómina (POO)

Actividad Unidad 3 – Universidad de Cartagena.
Sistema de nómina en Python con programación orientada a objetos para una
empresa con cuatro tipos de empleados, cada uno con su propia forma de calcular
salario, bonos, beneficios y deducciones.

## Cómo ejecutarlo

Requiere Python 3.9 o superior. No usa librerías externas.

  python main.py                          # demostración con 4 empleados
  python -m unittest discover -s tests -v # pruebas unitarias

## Estructura

  sistema-nomina/
  ├── main.py                      # demostración
  ├── nomina/
  │   ├── constantes.py            # reglas de negocio (porcentajes, umbrales)
  │   ├── excepciones.py           # errores del dominio
  │   ├── deducciones.py           # Deduccion (abstracta), PensionSeguroSocial, Arl
  │   ├── beneficios.py            # Beneficio (abstracto), BonoAlimentacion, FondoAhorro
  │   ├── empleados.py             # Empleado (abstracta) + 4 tipos de empleado
  │   ├── liquidacion.py           # resultado del cálculo (desprendible)
  │   └── servicio_nomina.py       # procesa la nómina de todos los empleados
  └── tests/                       # pruebas unitarias (unittest)

## Diseños y Principios SOLID aplicados

Principio                    | Dónde se ve
-----------------------------+---------------------------------------------------------------------------------------------------------------------
S – Responsabilidad única    | Empleado calcula su nómina; Deduccion y Beneficio tienen sus propias clases; ServicioNomina maneja el conjunto; Liquidacion solo guarda y presenta resultados.
O – Abierto/cerrado          | Un nuevo tipo de empleado, deducción o beneficio se agrega con una clase nueva, sin modificar las existentes.
L – Sustitución de Liskov    | ServicioNomina trata a todos como Empleado; cualquier subclase funciona en su lugar.
I – Segregación de interfaces| Deduccion y Beneficio son contratos pequeños de un solo método; ningún tipo está obligado a implementar lo que no usa.
D – Inversión de dependencias| Empleado recibe Deduccion por inyección y depende de la abstracción, no de las clases concretas.

Otros patrones y prácticas: polimorfismo, Template Method (liquidar()), constantes con nombre en lugar de números mágicos, validaciones con excepciones propias, docstrings y comentarios, y funciones pequeñas con un único propósito.

## Reglas de negocio implementadas

Tipo         | Salario                                        | Bonos                                  | Beneficios
-------------+------------------------------------------------+----------------------------------------+-----------------------------------------------------------
Asalariado   | Fijo mensual                                   | 10% del salario si tiene más de 5 años | Bono alimentación $1.000.000
Por horas    | Horas x tarifa; más de 40 h -> extras a 1.5x   | Ninguno                                | Fondo de ahorro 2% si tiene más de 1 año y lo acepta
Por comisión | Base + % de comisión sobre ventas              | 3% de las ventas si superan $20.000.000 | Bono alimentación $1.000.000
Temporal     | Fijo mensual (contrato a término definido)     | Ninguno                                | Ninguno

Deducciones para todos: Seguro Social y Pensión (4% del bruto) y ARL.

Validaciones: salario neto no negativo, horas no negativas, ventas no menores a $0 (además: tarifa, salario, antigüedad, porcentaje de comisión y duración del contrato). Se lanzan DatoInvalidoError o SalarioNetoNegativoError.

## Supuestos (el enunciado no los define)

1. ARL: no se indica la tasa. Se usa 0,522 % (riesgo I) y es configurable: Arl(tasa=...).
2. Salario bruto = salario base/devengado + bonos (incluye la comisión). Sobre ese valor se calcula el 4 %.
3. Beneficios (bono de alimentación y fondo de ahorro) son aportes de la empresa: se reportan aparte y no se suman al salario neto. Se incluyen en el costo total de la empresa.
4. Fórmula: neto = bruto - deducciones.
5. Porcentaje de comisión y antigüedad son datos de entrada de cada empleado.
6. Las horas extras se evalúan sobre el total de horas del período liquidado (límite de 40).
7. El fondo de ahorro se calcula sobre el salario bruto.

## Metodología de desarrollo de software

Se usó Scrum adaptado a un equipo de una persona, con iteraciones cortas (sprints) y entregas incrementales, apoyado en TDD ligero (pruebas junto con el código).

Producto (backlog) y sprints:

Sprint | Objetivo                        | Entregable
-------+---------------------------------+----------------------------------------------------------------------------
1      | Análisis de requisitos y diseño | Reglas de negocio, supuestos, diagrama de clases
2      | Núcleo del dominio              | Clase abstracta Empleado, deducciones y beneficios, con pruebas
3      | Tipos de empleado               | Asalariado, por horas, por comisión y temporal, con pruebas y validaciones
4      | Servicio y demostración         | ServicioNomina, main.py
5      | Refactorización y cierre        | Eliminación de duplicados, comentarios y README

Cómo se aplicó:
- Planeación: el enunciado se dividió en historias de usuario (ej. "Como empresa quiero que las horas extras se paguen a 1.5x para cumplir la regla de negocio").
- Ciclo de trabajo: cada historia se implementó con su prueba unitaria y se guardó con un commit pequeño.
- Revisión (retrospectiva): al final de cada sprint se revisó el código; de ahí salió la refactorización (constantes centralizadas, patrón Template Method, validación reutilizable).
- Control de versiones: Git/GitHub con commits descriptivos y rama main.
- Calidad: pruebas unitarias (valores límite incluidos: 5 años, 40 horas, $20.000.000) antes de dar una historia por terminada.

## Pruebas unitarias

38 pruebas con unittest que cubren: cálculo de cada tipo de empleado, valores límite, bonos, beneficios, deducciones, validaciones, error por salario neto negativo y el servicio de nómina.