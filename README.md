# **slashdot_media_senior_python_engineer_test**
A python test for the position: Senior Python Engineer at SlashDot Media, Inc.

## **Python Software Engineer Questions**

Please put your responses in line below in red.

[Questions 1]

#### Questions 1
Pretend that an API exists at https://example.com/api/products which returns:

            `[{"product": "Shoes", "price": 35, "rating": 4.2},
            {"product": "White Hat", "price": 21, "rating": 4.8},
            ...]`
            
1. Write a function in Python to consume this API.
2. Write another function for business logic to find all products rated 4 and above.
3. Write enough unit / integration tests to completely cover the code in both functions.

#### Answer 1:
<details>
<p>

##### Find answers in the three files in the answer folder

    INSTALLATION:
_Create a new python project and copy the files in the answer folder into the newly created project.
then install the following packages using pip._
    
    pip install pytest asyncio[standips] aiohttp
    pip install install pytest-asyncio pytest-austin pytest-cov
    
_To run test_

    python -m pytest test_product.py --asyncio-mode=strict --cov --profile-mode=all
   
  

</p>
</details>