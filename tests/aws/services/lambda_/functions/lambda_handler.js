exports.handler = async (event) => {
   console.log(JSON.stringify(event))
   return {
     statusCode: 200,
     body: JSON.stringify(`response from shipyard lambda: ${JSON.stringify(event)}`),
     isBase64Encoded: false,
     headers: {}
   }
}
