# Reporte Consolidado de Órdenes de Venta

Este módulo permite consolidar las líneas de múltiples Órdenes de Venta (`sale.order`) seleccionadas directamente desde la vista de lista, agrupando los productos por su categoría correspondiente, sumando las cantidades pedidas y generando un reporte PDF de forma instantánea.

## 🚀 Características
*   **Impresión Instantánea (Sin Asistentes Visuales):** Se omiten ventanas emergentes intermedias; al hacer clic en "Imprimir líneas de la orden" en el menú de acción, el reporte PDF se descarga inmediatamente en segundo plano.
*   **Agrupación y Consolidación Inteligente:** Agrupa las líneas de venta por su Categoría de Producto y por el Producto en sí. Suma las cantidades en una sola línea combinada de forma automática.
*   **Diseño Optimizado y U.M. incluida:** Muestra la columna "U.M." (Unidad de Medida) de los productos. Utiliza un formato de hoja estrecho A4 (márgenes de 10mm), filas compactas de baja altura para ahorrar papel y una fuente con un punto adicional para máxima legibilidad.
*   **Arquitectura Sólida:** Hace uso de un Asistente Transitorio (`TransientModel`) en segundo plano a través de una acción de servidor (`ir.actions.server`), permitiendo reutilizar y extender fácilmente la lógica de negocio en el futuro si se desean agregar filtros o configuraciones adicionales.

---

## 🛠️ Cómo incluir en un entorno de Odoo Enterprise

Para integrar este módulo en una instalación de **Odoo Enterprise** (on-premise, Odoo.sh, o servidor propio), sigue estos pasos:

### 1. Copiar el módulo al directorio de Addons
Copia el directorio completo `sale_order_consolidated_report` en tu carpeta de módulos personalizados (*custom addons*).

### 2. Configurar la ruta en `odoo.conf`
Asegúrate de que la ruta donde se encuentra la carpeta esté declarada dentro del parámetro `addons_path` en el archivo de configuración de Odoo (`odoo.conf`).
```ini
addons_path = /ruta/a/odoo/addons, /ruta/a/enterprise/addons, /ruta/a/tus/custom_addons
```

### 3. Reiniciar el Servidor de Odoo
Reinicia el proceso del servidor de Odoo Enterprise para que el sistema reconozca el nuevo directorio en disco.
*   En Linux/Ubuntu:
    ```bash
    sudo service odoo restart
    ```
*   O mediante comando directo de terminal en tu entorno de desarrollo o producción.

### 4. Actualizar la Lista de Aplicaciones en Odoo
1.  Inicia sesión en Odoo Enterprise con un usuario administrador.
2.  Activa el **Modo Desarrollador** (*Developer Mode*) desde Ajustes o mediante la URL de tu navegador (`?debug=1`).
3.  Ve al módulo de **Aplicaciones** (*Apps*).
4.  En el menú superior, haz clic en **Actualizar lista de aplicaciones** (*Update Apps List*) y luego presiona **Actualizar** (*Update*).

### 5. Instalar el Módulo
1.  En la barra de búsqueda de Aplicaciones, quita el filtro por defecto de *Aplicaciones* y escribe `sale_order_consolidated_report` (o el título del módulo `"Reporte Consolidado"`).
2.  Haz clic en el botón de **Activar** (*Install*).

---

## 📐 Estructura Técnica del Módulo
El módulo utiliza una estructura nativa de Odoo 19:

*   **`models/sale_consolidated_wizard.py`**: Contiene la lógica en Python que recibe la lista de órdenes activas (`active_ids`) mediante el contexto, consolida los productos calculando sumatorias y estructurando los diccionarios ordenados alfabéticamente para la vista QWeb.
*   **`views/sale_order_action.xml`**:
    *   Registra una acción de servidor (`ir.actions.server`) vinculada al menú de acción de `sale.order`.
    *   Desvincula explícitamente el asistente visual viejo (si existía) para garantizar la descarga instantánea.
*   **`report/report_action.xml`**: Define el reporte del motor QWeb (`ir.actions.report`) y lo vincula a un formato de papel personalizado (`report.paperformat`) de márgenes estrechos.
*   **`report/consolidated_report.xml`**: Plantilla XML/HTML de QWeb que le da los estilos visuales tipo rejilla, compactación de filas (rellenos de 5px) y tipografías aumentadas a 15px.
*   **`security/ir.model.access.csv`**: Asigna permisos correspondientes al asistente transitorio en cumplimiento con las directivas de seguridad de Odoo Enterprise.

## 📈 Flujo del Desarrollador (Actualizaciones futuras)
Si realizas modificaciones en las plantillas HTML (`consolidated_report.xml`) o en las acciones, recuerda que debes reiniciar y forzar la actualización del módulo especificando la base de datos de tu entorno enterprise:
```bash
python3 odoo-bin -d nombre_de_tu_bd -u sale_order_consolidated_report
```

---
*Módulo desarrollado y optimizado para entornos de impresión compacta de Odoo.*
