from setuptools import find_packages, setup  # type: ignore

setup(
    name="HelloWorld",
    version="1.1.1.beta10",
    packages=find_packages(),
    scripts=["say_hello.py"],
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["docutils>=0.3"],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"],
        # And include any *.msg files found in the "hello" package, too:
        "hello": ["*.msg"],
    },
)
