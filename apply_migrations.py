#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para aplicar migraciones de Alembic."""

import sys
from alembic.config import Config
from alembic import command

def main():
    """Aplicar todas las migraciones pendientes."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    print("✅ Migraciones aplicadas exitosamente.")

if __name__ == "__main__":
    main()
