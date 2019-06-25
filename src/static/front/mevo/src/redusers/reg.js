export default function reg(state = [], action){
  switch (action.type) {
    case 'REG_USER':
      return action.data
    default:
      return state;
  }
}