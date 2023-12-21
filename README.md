# StuddyBuddy
 An AI-Powered Teaching Assistant for O level Students; Math, English, Chinese, Science
 Currently in an interactive Telegram bot. 
 It leverages the power of OpenAI's GPT models and the Mathpix API to provide detailed answers to questions submitted either as text or images.

## Features

- Subject-specific assistance: Math, English, Science, and Chinese.
- Image processing for math problem recognition using Mathpix.
- Integration with OpenAI's GPT models for detailed and accurate answers.

### Try it out

[@L_bearbot](https://t.me/Lbear_bot)https://t.me/Lbear_bot



### Setting up the Configuration
If you would like to clone and run it locally, you will need to setup the following configure file and get the following api keys/ID/Tokens. 
Create a `config.json` file in the root directory with the following structure:

```json
{
    "telegram_token": "your_telegram_token",
    "mathpix_app_id": "your_mathpix_id",
    "mathpix_app_key": "your_mathpix_key",
    "openai_api_key": "your_openai_api_key"
}
