import request from './request'

// 添加星星
export function addStar(data) {
  return request({
    url: '/api/elf/add_star',
    method: 'post',
    data
  })
}

// 查询精灵等级
export function queryLevel(data) {
  return request({
    url: '/api/elf/query_level',
    method: 'post',
    data
  })
}

// 修改精灵等级
export function changeLevel(data) {
  return request({
    url: '/api/elf/change_level',
    method: 'post',
    data
  })
}

// 精灵结课
export function createEndClass(data) {
  return request({
    url: '/api/elf/create_endclass',
    method: 'post',
    data
  })
}

// 查询精灵任务
export function queryTask(data) {
  return request({
    url: '/api/elf/query_task',
    method: 'post',
    data
  })
}

// 删除精灵任务
export function deleteTask(data) {
  return request({
    url: '/api/elf/delete_task',
    method: 'post',
    data
  })
}

// 管理排行榜
export function manageRank(data) {
  return request({
    url: '/api/elf/manage_rank',
    method: 'post',
    data
  })
}
