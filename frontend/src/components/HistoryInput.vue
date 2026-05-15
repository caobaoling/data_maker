<template>
  <el-autocomplete
    v-model="inputValue"
    :fetch-suggestions="fetchSuggestions"
    :placeholder="placeholder"
    :clearable="clearable"
    :style="inputStyle"
    :disabled="disabled"
    popper-class="history-input-popper"
    @select="handleSelect"
    @change="handleChange"
    @blur="handleBlur"
  >
    <template v-if="$slots.prepend" #prepend>
      <slot name="prepend" />
    </template>
    <template v-if="$slots.append" #append>
      <slot name="append" />
    </template>
  </el-autocomplete>
</template>

<script setup>
import { computed } from 'vue'
import { saveHistory, useFetchSuggestions } from '@/composables/useInputHistory'

const props = defineProps({
  modelValue: { type: String, default: '' },
  storageKey: { type: String, required: true }, // 唯一标识，用于区分不同输入框
  placeholder: { type: String, default: '请输入' },
  clearable: { type: Boolean, default: true },
  disabled: { type: Boolean, default: false },
  style: { type: [String, Object], default: '' }
})

const emit = defineEmits(['update:modelValue', 'change', 'select'])

const inputValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const inputStyle = computed(() => props.style || '')

const fetchSuggestions = useFetchSuggestions(props.storageKey)

const handleSelect = (item) => {
  emit('update:modelValue', item.value)
  emit('select', item.value)
}

const handleChange = (val) => {
  emit('change', val)
}

// 失焦时保存历史
const handleBlur = () => {
  if (inputValue.value?.trim()) {
    saveHistory(props.storageKey, inputValue.value)
  }
}
</script>

<style>
.history-input-popper .el-autocomplete-suggestion__list li {
  font-size: 13px;
  color: #606266;
}
</style>
