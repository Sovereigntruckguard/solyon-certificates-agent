from multi_tool_agent.agent import generar_certificado

print("============ INICIANDO PRUEBA LOCAL CON DOBLE CORREO ============")

# Llamamos a la función inyectando el correo de Elizabeth como cliente
resultado = generar_certificado(
    dot="1234567",  
    holder_nombre="EMPRESA DE PRUEBA LLC",
    holder_direccion="777 Test Avenue, Suite 100",
    holder_ciudad_estado_zip="Miami, FL 33101",
    email_cliente="e-liz-08@hotmail.com",  # <-- El correo de Elizabeth para la prueba
    email_broker="info@sovereigntruckguard.com"   # <-- Tu correo corporativo
)

print("\nResultado de la ejecución:")
print(resultado)
print("=================================================================")