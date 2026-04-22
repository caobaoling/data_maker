import request from './request'

// 添加订单
export function addOrder(data) {
  return request({
    url: '/api/order/add',
    method: 'post',
    data
  })
}
