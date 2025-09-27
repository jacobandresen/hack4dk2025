#!/usr/bin/env python3
"""
Setup script for SMK MCP Server
"""

from setuptools import setup, find_packages

setup(
    name="smk-mcp-server",
    version="1.0.0",
    description="MCP Server for SMK (Statens Museum for Kunst) API",
    author="SMK MCP Team",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
        "httpx>=0.25.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "smk-mcp-server=smk_mcp_server:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

