from setuptools import setup, find_packages

setup(
    name='gptchain',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'openai>=1.2.3'
    ],
    entry_points={
        'console_scripts': [
            'gptchain=gptchain:gptchain',
        ],
    },
    author='Mark Shust',
    author_email='mark@shust.com',
    description='Link multiple GPT prompts into a chain of responses.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/markshust/gptchain',
)
