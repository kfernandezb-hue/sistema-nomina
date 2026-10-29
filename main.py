"""Demostracion del sistema de nomina."""
from nomina import (
    EmpleadoAsalariado,
    EmpleadoPorComision,
    EmpleadoPorHoras,
    EmpleadoTemporal,
    ServicioNomina,
)
from nomina.liquidacion import formatear_pesos


def main() -> None:
    servicio = ServicioNomina()
    servicio.agregar_empleado(
        EmpleadoAsalariado("Ana Torres", "1001", 4_000_000, anios_antiguedad=7)
    )
    servicio.agregar_empleado(
        EmpleadoPorHoras("Luis Perez", "1002", horas_trabajadas=48, tarifa_hora=20_000,
                         anios_antiguedad=2, acepta_fondo_ahorro=True)
    )
    servicio.agregar_empleado(
        EmpleadoPorComision("Marta Diaz", "1003", salario_base=1_800_000,
                            porcentaje_comision=0.05, ventas=25_000_000)
    )
    servicio.agregar_empleado(
        EmpleadoTemporal("Carlos Ruiz", "1004", 2_000_000, duracion_contrato_meses=6)
    )

    for liquidacion in servicio.liquidar_todos():
        print(liquidacion.resumen())
        print()

    print("=" * 40)
    print(f"Total salarios netos : {formatear_pesos(servicio.total_salarios_netos())}")
    print(f"Costo total empresa  : {formatear_pesos(servicio.costo_total_empresa())}")


if __name__ == "__main__":
    main()