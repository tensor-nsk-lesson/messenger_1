export default function auth(state = [], action){
  switch (action.type) {
    case 'AUTH_USER':
      return action.key
    default:
      return state;
  }
}