/**
 * 输入历史记录 composable
 * 基于 localStorage 缓存每个输入框的历史输入值
 */

const MAX_HISTORY = 10 // 每个 key 最多保留10条历史

/**
 * 读取某个 key 的历史记录
 * @param {string} storageKey
 * @returns {string[]}
 */
export function getHistory(storageKey) {
  try {
    return JSON.parse(localStorage.getItem(storageKey) || '[]')
  } catch {
    return []
  }
}

/**
 * 保存一条输入值到历史记录
 * @param {string} storageKey
 * @param {string} value
 */
export function saveHistory(storageKey, value) {
  if (!value || !value.trim()) return
  const trimmed = value.trim()
  const history = getHistory(storageKey)
  // 去重：已存在则移到最前
  const filtered = history.filter(v => v !== trimmed)
  filtered.unshift(trimmed)
  localStorage.setItem(storageKey, JSON.stringify(filtered.slice(0, MAX_HISTORY)))
}

/**
 * 生成 el-autocomplete 需要的 fetchSuggestions 函数
 * @param {string} storageKey
 * @returns {Function}
 */
export function useFetchSuggestions(storageKey) {
  return (queryString, cb) => {
    const history = getHistory(storageKey)
    const results = queryString
      ? history.filter(v => v.includes(queryString))
      : history
    cb(results.map(v => ({ value: v })))
  }
}
