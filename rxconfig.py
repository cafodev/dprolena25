import reflex as rx

config = rx.Config(
    app_name="chatbot",
    # ⚠️ IMPORTANTE: Para acceso en red local, cambia 'localhost' por tu IP local (ej. 192.168.1.X)
     api_url="http://192.168.10.202:8000",
    
    # Permitir orígenes cruzados para acceso en red
    cors_allowed_origins=["*"],
    
    # Deshabilitar sitemap plugin para evitar el warning
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin']
)
