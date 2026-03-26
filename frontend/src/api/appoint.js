import request from './request'

// 获取一级教材列表(Level列表)
export function getTextbookLevels() {
  return request({
    url: '/api/appoint/textbooks',
    method: 'get',
    params: { type: 'level' }
  })
}

// 获取二级单元列表(根据top_id)
export function getTextbookUnits(topId) {
  return request({
    url: '/api/appoint/textbooks',
    method: 'get',
    params: { type: 'units', top_id: topId }
  })
}

// 获取三级课程列表(根据sub_id)
export function getTextbookLessons(subId) {
  return request({
    url: '/api/appoint/textbooks',
    method: 'get',
    params: { type: 'lessons', sub_id: subId }
  })
}

// 统一添加预约接口 (支持普通话/英语/阿语)
export function addAppoint(data) {
  return request({
    url: '/api/appoint/add',
    method: 'post',
    data
  })
}

// 兼容旧版本(保留旧函数名)
export function addAppointCn(data) {
  return addAppoint(data)
}

export function addAppointEn(data) {
  return addAppoint(data)
}

// 查询预约列表
export function getAppointList(params) {
  return request({
    url: '/api/appoint/list',
    method: 'get',
    params
  })
}

// 修改预约状态
export function updateAppointStatus(data) {
  return request({
    url: '/api/appoint/update_status',
    method: 'post',
    data
  })
}

// 给预约打星
export function addAppointStar(data) {
  return request({
    url: '/api/appoint/add_star',
    method: 'post',
    data
  })
}
