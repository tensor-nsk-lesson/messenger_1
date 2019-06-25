export function fetchSuccess(key){
  localStorage.setItem('success',JSON.stringify(key.success));
    return {
      type: 'AUTH_USER',
      key
    }
  }

  
export function auth(url, data){
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
    .then(data => dispatch(fetchSuccess(data)))
    .catch(() => {})
  }
}