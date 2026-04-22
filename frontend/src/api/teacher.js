import request from './request'

// 添加合同
export function addContract(data) {
  return request({
    url: '/api/teacher/add_contract',
    method: 'post',
    data
  })
}

// 查询合同
export function queryContract(data) {
  return request({
    url: '/api/teacher/query_contract',
    method: 'post',
    data
  })
}

// 获取老师邮箱
export function getTeacherEmail(data) {
  return request({
    url: '/api/teacher/get_email',
    method: 'post',
    data
  })
}

// 重置老师密码
export function resetTeacherPassword(data) {
  return request({
    url: '/api/teacher/reset_password',
    method: 'post',
    data
  })
}
