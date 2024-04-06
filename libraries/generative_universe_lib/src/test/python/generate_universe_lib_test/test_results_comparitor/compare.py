import io
import os
import numpy as np
from PIL import Image


class TestResultComparator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.generate_test_results = os.getenv('GENERATE_TEST_RESULTS', 'true').lower() == 'true'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def compare_or_save_image(self, image_bytes):
        if self.generate_test_results:
            with open(self.file_name, 'wb') as f:
                f.write(image_bytes)
        else:
            with open(self.file_name, 'rb') as f:
                expected_bytes = f.read()
                expected_image = Image.open(io.BytesIO(expected_bytes))
                actual_image = Image.open(io.BytesIO(image_bytes))
                np.testing.assert_array_almost_equal(np.array(expected_image),
                                                     np.array(actual_image),
                                                     decimal=5,
                                                     err_msg=f"Image comparison failed for {self.file_name}")
