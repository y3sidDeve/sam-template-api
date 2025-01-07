# API de Procesamiento de Transacciones Serverless

Este proyecto implementa una API serverless para la creación y gestión de transacciones financieras utilizando AWS Lambda y API Gateway.

La aplicación está construida usando el Modelo de Aplicaciones Serverless de AWS (SAM) y proporciona un endpoint sencillo para crear nuevas transacciones. Demuestra el uso de principios de diseño orientados al dominio al separar la lógica de dominio (entidad transacción) de las preocupaciones de infraestructura (manejo de la API).

La API está diseñada para ser escalable y fácilmente extensible, lo que la hace adecuada para diversos tipos de Testing.

## Estructura del Repositorio

```
.
├── __init__.py
├── events
│   └── event.json
├── README.md
├── simu_app
│   ├── __init__.py
│   ├── domain
│   │   └── entities
│   │       └── transaction.py
│   └── infrastructure
│       └── api
│           └── create_transaction.py
├── template.yaml
└── tests
    ├── __init__.py
    ├── integration
    │   ├── __init__.py
    │   └── test_api_gateway.py
    └── unit
        ├── __init__.py
        └── test_handler.py
```

### Archivos Clave:
- `template.yaml`: Plantilla SAM que define los recursos de AWS y la configuración de la API.
- `simu_app/domain/entities/transaction.py`: Contiene la definición de la entidad Transacción.
- `simu_app/infrastructure/api/create_transaction.py`: Manejador Lambda para la creación de transacciones.
- `tests/integration/test_api_gateway.py`: Pruebas de integración para API Gateway.
- `tests/unit/test_handler.py`: Pruebas unitarias para el manejador Lambda.

## Instrucciones de Uso

### Requisitos Previos
- AWS CLI instalado y configurado.
- AWS SAM CLI instalado.
- Python 3.12.

### Instalación

1. Clonar el repositorio:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Desplegar la aplicación:
   ```
   sam build
   sam deploy --guided
   ```

   Siga las indicaciones para configurar los ajustes de despliegue.

### Pruebas

Para ejecutar pruebas unitarias:
```
python -m pytest tests/unit
```

Para ejecutar pruebas de integración:
```
export AWS_SAM_STACK_NAME=<your-stack-name>
python -m pytest tests/integration
```

### Uso de la API

Después del despliegue, puede crear una nueva transacción enviando una solicitud GET al endpoint `/new-transaction`. La URL de API Gateway se proporcionará en las salidas del stack de CloudFormation.

Ejemplo usando curl:
```
curl https://<api-id>.execute-api.<region>.amazonaws.com/Prod/new-transaction/
```

### Solución de Problemas

1. Errores 5xx en API Gateway:
   - Verifique los Logs de CloudWatch para la función Lambda.
   - Asegúrese de que la función Lambda tenga los permisos correctos.

2. Fallos en el despliegue:
   - Verifique que sus credenciales de AWS estén configuradas correctamente.
   - Compruebe si hay errores de sintaxis en la plantilla SAM.

3. Fallos en pruebas de integración:
   - Asegúrese de que la variable de entorno `AWS_SAM_STACK_NAME` esté configurada correctamente.
   - Verifique que el endpoint de API Gateway sea accesible.

Para habilitar registros detallados para la función Lambda, modifique el archivo `template.yaml`:

```yaml
Resources:
  TransactionFunction:
    Properties:
      Environment:
        Variables:
          LOG_LEVEL: DEBUG
```

Luego, vuelva a desplegar la aplicación.

## Flujo de Datos

El flujo de datos de la solicitud a través de la aplicación sigue estos pasos:

1. El cliente envía una solicitud GET al endpoint `/new-transaction` de API Gateway.
2. API Gateway reenvía la solicitud a la función Lambda `TransactionFunction`.
3. El manejador Lambda en `create_transaction.py` procesa la solicitud.
4. Se crea una nueva entidad Transacción usando la clase `Transaction` de `transaction.py`.
5. La transacción se valida y procesa (en este ejemplo, es solo una respuesta simulada).
6. La función Lambda devuelve una respuesta, que se envía de vuelta a través de API Gateway al cliente.

```
Cliente -> API Gateway -> Lambda (TransactionFunction) -> Entidad Transacción -> Lambda -> API Gateway -> Cliente
```

Nota: La implementación actual no incluye persistencia de datos real. En un entorno de producción, típicamente se agregaría un paso de interacción con la base de datos después de la creación de la entidad Transacción.

## Infraestructura

La infraestructura para este proyecto está definida en el archivo `template.yaml` usando AWS SAM. Los recursos clave incluyen:

- Lambda:
  - TransactionFunction: Maneja la creación de nuevas transacciones.
    - Runtime: Python 3.12.
    - Handler: `infrastructure.api.create_transaction.lambda_handler`.
    - Timeout: 3 segundos.
    - Logging: Formato JSON.

- API Gateway:
  - Endpoint: `/new-transaction` (método GET).
  - Integrado con `TransactionFunction`.

La plantilla SAM también define salidas para la URL de API Gateway, el ARN de la función Lambda y el ARN del rol IAM, que pueden ser útiles para configuraciones de integración o monitoreo adicionales.

