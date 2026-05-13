#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de migración: SQLite → PostgreSQL

Uso:
    python migrate_to_postgres.py --host localhost --user postgres --password ... --database taskflow
"""

import asyncio
import argparse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


async def migrate_database(
    source_url: str,
    target_url: str
) -> None:
    """Migra datos de una BD a otra."""
    
    print(f"📋 Origen:  {source_url[:50]}...")
    print(f"📋 Destino: {target_url[:50]}...")
    
    try:
        # Crear engines
        source_engine = create_async_engine(source_url, echo=False)
        target_engine = create_async_engine(target_url, echo=False)
        
        async with source_engine.connect() as source_conn:
            async with target_engine.connect() as target_conn:
                # Leer datos de usuarios
                usuarios_result = await source_conn.execute(text(
                    "SELECT id, username, email, hashed_password, nombre_completo, activo FROM usuarios"
                ))
                usuarios = usuarios_result.fetchall()
                
                if usuarios:
                    print(f"👥 Migrando {len(usuarios)} usuario(s)...")
                    for u in usuarios:
                        await target_conn.execute(text(
                            "INSERT INTO usuarios (id, username, email, hashed_password, nombre_completo, activo) "
                            "VALUES (:id, :username, :email, :hashed_password, :nombre_completo, :activo)"
                        ), {
                            "id": u[0],
                            "username": u[1],
                            "email": u[2],
                            "hashed_password": u[3],
                            "nombre_completo": u[4],
                            "activo": u[5]
                        })
                    await target_conn.commit()
                
                # Leer datos de proyectos
                proyectos_result = await source_conn.execute(text(
                    "SELECT id, nombre, descripcion, usuario_id FROM proyectos"
                ))
                proyectos = proyectos_result.fetchall()
                
                if proyectos:
                    print(f"📁 Migrando {len(proyectos)} proyecto(s)...")
                    for p in proyectos:
                        await target_conn.execute(text(
                            "INSERT INTO proyectos (id, nombre, descripcion, usuario_id) "
                            "VALUES (:id, :nombre, :descripcion, :usuario_id)"
                        ), {
                            "id": p[0],
                            "nombre": p[1],
                            "descripcion": p[2],
                            "usuario_id": p[3]
                        })
                    await target_conn.commit()
                
                # Leer datos de tareas
                tareas_result = await source_conn.execute(text(
                    "SELECT id, titulo, descripcion, prioridad, estado, proyecto_id FROM tareas"
                ))
                tareas = tareas_result.fetchall()
                
                if tareas:
                    print(f"✓ Migrando {len(tareas)} tarea(s)...")
                    for t in tareas:
                        await target_conn.execute(text(
                            "INSERT INTO tareas (id, titulo, descripcion, prioridad, estado, proyecto_id) "
                            "VALUES (:id, :titulo, :descripcion, :prioridad, :estado, :proyecto_id)"
                        ), {
                            "id": t[0],
                            "titulo": t[1],
                            "descripcion": t[2],
                            "prioridad": t[3],
                            "estado": t[4],
                            "proyecto_id": t[5]
                        })
                    await target_conn.commit()
        
        print("\n✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"\n❌ Error durante migración: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await source_engine.dispose()
        await target_engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Migra datos de SQLite a PostgreSQL"
    )
    parser.add_argument(
        "--source",
        default="sqlite+aiosqlite:///./taskflow.db",
        help="URL de origen (SQLite por defecto)"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host de PostgreSQL"
    )
    parser.add_argument(
        "--port",
        default="5432",
        help="Puerto de PostgreSQL"
    )
    parser.add_argument(
        "--user",
        default="postgres",
        help="Usuario de PostgreSQL"
    )
    parser.add_argument(
        "--password",
        required=True,
        help="Contraseña de PostgreSQL"
    )
    parser.add_argument(
        "--database",
        default="taskflow",
        help="Nombre de la BD destino"
    )
    
    args = parser.parse_args()
    
    target_url = f"postgresql+psycopg://{args.user}:{args.password}@{args.host}:{args.port}/{args.database}"
    
    asyncio.run(migrate_database(args.source, target_url))
