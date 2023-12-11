// Type of command
// 1. navigate: go to another page
export const type = {
    navigate: 'navigate'
}

export const Keyword = [
    {keyword: 'đăng nhập', type: type.navigate, path: 'Login'},
    {keyword: 'đăng ký', type: type.navigate, path: 'Register'},
    {keyword: 'mặt người', type: type.navigate, path: 'FaceRegister'},
    {keyword: 'trang chủ', type: type.navigate, path: 'Home'},
]