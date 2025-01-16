interface LambdaResponse {
  message: string;
  is_book?: boolean;
  creator_id?: string;
  finished?: boolean;
}

const LAMBDA_PREFIX = 'https://yh8cmasjvk.execute-api.us-west-2.amazonaws.com/prod/';

const CREATE_CREATOR_LAMBDA_URL = LAMBDA_PREFIX + 'create-offer-creator';
const CHAT_LAMBDA_URL = LAMBDA_PREFIX + 'check-input';

const IS_BOOK_LAMBDA_URL = LAMBDA_PREFIX + 'categorize-object';
const ANALYZE_BOOK_LAMBDA_URL = LAMBDA_PREFIX + 'define-object';
const PROMPT_LAMBDA_URL = LAMBDA_PREFIX + 'prompt';

export async function sendToLambda<T>(data: T, lambdaUrl: string): Promise<LambdaResponse> {
  try {
    console.log("sending to lambda: ", lambdaUrl, " with data: ", data)
    const response = await fetch(lambdaUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    console.log("response: ", response)
    const result = await response.json();
    console.log("result: ", result)
    return result;
  } catch (error) {
    console.error('Error sending data to Lambda:', error);
    throw error;
  }
}

export async function createCreator<T>(data: T): Promise<LambdaResponse> {
    // Create creator
    console.log("creating creator with data: ", data)
    const creator_response = await fetch(CREATE_CREATOR_LAMBDA_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    console.log("creator_response: ", creator_response)
    return creator_response.json();
}

export async function sendToAWS<T>(data: T): Promise<LambdaResponse>{

  // Send text message to chat
//   const chat_response = await fetch(CHAT_LAMBDA_URL, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify(data),
//   });

//   console.log("chat_response: ", chat_response)
//   return chat_response.json();
  return {
    message: "Hello, send image of an item to get started.",
    is_book: false,
    creator_id: "123"
  }
}

export async function sendImageToChat<T>(data: T): Promise<LambdaResponse>{
    // Send image message to chat
    // return {
    //     message: "Hello, send image of an item to get started.",
    //     is_book: false,
    //     creator_id: "123"
    // }

    const is_book_response = await fetch(IS_BOOK_LAMBDA_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

    const chat_response_raw = await is_book_response.json()
    const chat_response = JSON.parse(chat_response_raw)
    
    console.log("chat_response is book prompt: ", typeof chat_response)
    console.log("chat_response is book prompt: ", chat_response)
    const is_book = chat_response.is_book;
    if (is_book === false) {
        return {
            message: chat_response.answer,
            is_book: false
        }
    } 

    // Analyze book
    const book_data = await fetch(ANALYZE_BOOK_LAMBDA_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

    console.log("book_data: ", book_data)

    return {
        message: "Image has been analyzed",
        is_book: true,
        creator_id: "123"
    }


    // // Get prompt for user
    // const prompt_response = await fetch(PROMPT_LAMBDA_URL, {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify(data),
    // })

    // const prompt_response_json = await prompt_response.json();
    // if (prompt_response_json.finished) {
    //     return {
    //         message: "All data has been collected, your offer is ready to be created.",
    //         is_book: true,
    //         creator_id: "123"
    //     }
    // }

    // return prompt_response.json();
}

export default { sendToAWS, sendImageToChat }; 