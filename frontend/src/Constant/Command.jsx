// Type of command
// 1. navigate: go to another page
export const type = {
    navigate: 'navigate'
}

// Auth rank:
// -1: Can only be accessed when not logged in
// 1: Can only be accessed when logged in
// 0: Not care
export const Keyword = [
    {keyword: 'đăng nhập', type: type.navigate, path: 'Login', authRank: -1},
    {keyword: 'đăng ký', type: type.navigate, path: 'Register', authRank: -1},
    {keyword: 'mặt người', type: type.navigate, path: 'FaceRegister', authRank: 1},
    {keyword: 'trang chủ', type: type.navigate, path: 'Home', authRank: 0},
]