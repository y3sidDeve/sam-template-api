# Plantilla Serverless con Arquitectura Hexagonal

## Descripción

Esta plantilla serverless está diseñada como un punto de partida para construir proyectos que sigan principios de la arquitectura hexagonal. Incluye un conjunto básico de funciones CRUD (Crear, Leer, Actualizar y Eliminar) para usuarios, lo cual sirve como ejemplo para exponer las capacidades de la arquitectura y las APIs. Está optimizada para implementaciones en entornos serverless como AWS Lambda, utilizando DynamoDB como base de datos.

### Características principales

- **Arquitectura Hexagonal**: Separación clara de responsabilidades en capas:
  - **Application**: Contiene los casos de uso del dominio.
  - **Core**: Define las entidades y los puertos necesarios para la interacción con los adaptadores.
  - **Infrastructure**: Implementa los adaptadores necesarios para la API y la interacción con la base de datos.

- **Compatibilidad Serverless**: Optimizada para servicios como AWS Lambda y DynamoDB.
- **Código Modular y Escalable**: Organizado para facilitar la extensión del proyecto.

## Estructura del Proyecto

```plaintext
│   requirements.txt
│   __init__.py
│
├───application
│   └───use_cases
│           create_user.py
│           get_all_users.py
│           get_user_by_id.py
│
├───core
│   ├───entities
│   │       transaction.py
│   │       user.py
│   │       __init__.py
│   │
│   └───ports
│           user_repository.py
│           __init__.py
│
└───infrastructure
    │   __init__.py
    │
    ├───api
    │       create_transaction.py
    │       create_user.py
    │       get_all_users.py
    │       get_user.py
    │       __init__.py
    │
    └───repositories
            dynamodb_user_repository.py
            __init__.py
```

## Instrucciones Generales

1. **Instalar dependencias**:
   Asegúrate de tener Python instalado. Luego, instala las dependencias ejecutando:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar las credenciales de AWS**:
   Configura las credenciales necesarias para acceder a los servicios de AWS.
   ```bash
   aws configure
   ```

3. **Desplegar en AWS**:
   Puedes usar herramientas como `Serverless Framework`, `AWS SAM`, o `AWS CDK` para desplegar esta plantilla. Asegúrate de definir las funciones y sus permisos en el archivo correspondiente (por ejemplo, `serverless.yml` o `template.yaml`).

4. **Ejecutar localmente**:
   Utiliza herramientas como `sam local` o `serverless invoke local` para probar las funciones antes de desplegarlas.

5. **Extender el proyecto**:
   - Agrega nuevos casos de uso en la capa `application/use_cases`.
   - Define nuevas entidades o puertos en `core/entities` y `core/ports`.
   - Implementa adaptadores adicionales en `infrastructure`.

## Contribuciones

Esta plantilla está diseñada para ser un punto de partida flexible. Siéntete libre de personalizarla y adaptarla según tus necesidades.

---

Con esta base, puedes desarrollar rápidamente aplicaciones escalables y bien organizadas siguiendo los principios de la arquitectura hexagonal.

