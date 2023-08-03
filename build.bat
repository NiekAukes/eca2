rmdir /s /q dist
py -m build
py -m twine upload --repository pypi dist/* --username __token__ --password pypi-AgEIcHlwaS5vcmcCJDE3ZjJjYTNmLTYyZjYtNDgzNi1iN2MyLTk0MzQzMmFlOTEyOAACKlszLCI3MWZlNzlhNy1kMDBjLTQ3YmYtYmRhMC0xZmJmMjIxNjlhMDciXQAABiBpPFkgMfXyDilnFfPZbpKZcx_sDm3vcpxObNbsuCP1fg
