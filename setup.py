from setuptools import find_packages
from setuptools import setup

packages = find_packages()

with open('requirements.txt', 'r', encoding='UTF-8') as f:
    requirements = f.read().split()

setup(
    name='core',
    version='1.0.2',
    author='Kakorinis',
    author_email='newstyle-ps@yandex.ru',
    url='https://github.com/kakorinis/core.git',
    keywords='core',
    description='Core for microservices',
    long_description='Core for microservices',
    long_description_content_type='text/markdown',
    packages=packages,
    package_data={package: ['py.typed'] for package in packages},
    include_package_data=True,
    install_requires=None,  # requirements,  # если запуск не из контейнера
    classifiers=[
        'Natural Language :: Russian',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires='>=3.8',
    project_urls={
        'github': 'https://github.com/kakorinis/core.git',
    },
    setup_requires=['setuptools-git-versioning']
)
