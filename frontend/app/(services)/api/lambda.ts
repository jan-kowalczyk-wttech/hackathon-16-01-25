interface LambdaResponse {
  message: string;
  is_image: boolean;
}

const CREATE_CREATOR_LAMBDA_URL = '';
const CHAT_LAMBDA_URL = 'https://5yalyra1rl.execute-api.us-west-2.amazonaws.com/prod/check-input';

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

export async function sendToAWS<T>(data: T): Promise<LambdaResponse> {
    // Create creator
  const creator_response = await fetch(CREATE_CREATOR_LAMBDA_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  console.log("creator_response: ", creator_response)

  // Get chat response
  const chat_response = await fetch(CHAT_LAMBDA_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  console.log("chat_response: ", chat_response)
  return chat_response.json();
}

export default { sendToAWS }; 