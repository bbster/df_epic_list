<template>
  <div>
    <h2>Todo List</h2>
    <div>
      <input type="text" placeholder="할일을 입력하세요" />
      <span>
        <button type="button">추가</button>
      </span>
    </div>
    <ul>
      <li v-for="{ name } in todos" :key="name">
        {{ name }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      todos: [
        {
          name: "청소",
        },
        {
          name: "블로그 쓰기",
        },
        {
          name: "밥먹기",
        },
        {
          name: "안녕",
        },
      ],
    };
  },
  async mounted() {
    console.log(await this.$axios.get("/list/quantity"));
  },
};
</script>