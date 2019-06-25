export function regSuccess(data){
  return {
    type: 'REG_USER',
    data
  }
}
  
export default function reg(url, data){
  return (dispatch) => {
    return fetch(url, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
    })
    .then(response =>{
      if(!response.ok){
        throw new Error(response.statusText)
      }
      return response;
    })
    .then(response => response.json())
    .then(data => dispatch(regSuccess(data)))
    .catch(() => {})
  }
}