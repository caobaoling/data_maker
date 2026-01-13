import request from './request'

// 添加普通话预约
export function addAppointCn(data) {
  return request({
    url: '/appoint/add_cn',
    method: 'post',
    data
  })
}

// 添加英语预约
export function addAppointEn(data) {
  return request({
    url: '/appoint/add_en',
    method: 'post',
    data
  })
}

// 查询预约列表
export function getAppointList(params) {
  return request({
    url: '/appoint/list',
    method: 'get',
    params
  })
}

// 修改预约状态
export function updateAppointStatus(data) {
  return request({
    url: '/appoint/update_status',
    method: 'post',
    data
  })
}
