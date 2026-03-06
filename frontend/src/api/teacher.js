import request from './request'

// 添加前合同
export function addPreContract(data) {
  return request({
    url: '/api/teacher/add_pre_contract',
    method: 'post',
    data
  })
}

// 查询前合同
export function queryPreContract(data) {
  return request({
    url: '/api/teacher/query_pre_contract',
    method: 'post',
    data
  })
}
