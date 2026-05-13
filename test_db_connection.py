#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script de prueba de conexión a la base de datos."""

import os
import asyncio
import re
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()


async def test_connection() -> None:
    """Prueba la conexión a la base de datos."""
    
    # Obtener URL
    database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./taskflow.db")
    
    # Convertir PostgreSQL para async support
    if "postgresql:" in database_url:
        database_url = re.sub(r"^postgresql:", "postgresql+psycopg:", database_url)
    
    print(f"📌 Conectando a: {database_url[:50]}...")
    
    try:
        # Crear engine
        engine = create_async_engine(
            database_url,
            echo=False,
            pool_pre_ping=True,
        )
        
        # Probar conexión
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 'Conexión exitosa ✓'"))
            print(f"✅ {result.fetchone()[0]}")
            
            # Verificar tablas
            if "sqlite" in database_url:
                result = await conn.execute(text(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ))
            else:
                result = await conn.execute(text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
                ))
            
            tables = result.fetchall()
            print(f"📊 Tablas encontradas: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
        
        await engine.dispose()
        print("\n✓ Conexión cerrada correctamente")
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_connection())
