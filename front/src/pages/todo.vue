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
    <ul>
      {{
        aaa
      }}
      <li v-for="{ data } in aaa" :key="data">
        {{ data.count }}
        {{ data.items_object }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      aaa: "",
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
    this.aaa = await this.$axios.get("/list/quantity/?start_date=2020-10-01");
  },
};
</script>