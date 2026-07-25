<template>
  <div class="container mt-4">
    <h2 class="mb-4">Students</h2>

    <input
      v-model="search"
      class="form-control mb-3"
      placeholder="Search Student"
    />

    <table class="table table-bordered">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="student in filteredStudents"
          :key="student.id"
        >
          <td>{{ student.id }}</td>
          <td>{{ student.username }}</td>

          <td>
            <button
              v-if="!student.blacklisted"
              class="btn btn-danger btn-sm"
              @click="blacklist(student.id)"
            >
              Blacklist
            </button>

            <button
              v-else
              class="btn btn-secondary btn-sm"
              disabled
            >
              Blacklisted
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      students: [],
      search: ""
    };
  },

  computed: {
    filteredStudents() {
      return this.students.filter(student =>
        student.username
          .toLowerCase()
          .includes(this.search.toLowerCase())
      );
    }
  },

  mounted() {
    this.loadStudents();
  },

  methods: {
    async loadStudents() {
      const response = await fetch(`${this.$apiBase}/admin/students`, {
        credentials: "include"
      });

      const data = await response.json();
      this.students = data.students;
    },

    async blacklist(id) {
      const response = await fetch(
        `${this.$apiBase}/admin/student/${id}/blacklist`,
        {
          method: "POST",
          credentials: "include"
        }
      );

      const data = await response.json();
      alert(data.message);

      this.loadStudents();
    }
  }
};
</script>