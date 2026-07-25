<template>
  <div>
    <h2 class="mb-4">Companies</h2>

    <input
      v-model="search"
      class="form-control mb-3"
      placeholder="Search Company"
    />

    <table class="table table-bordered shadow">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Company Name</th>
          <th>Approve</th>
          <th>Reject</th>
          <th>Blacklist</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="company in filteredCompanies"
          :key="company.id"
        >
          <td>{{ company.id }}</td>
          <td>{{ company.companyname }}</td>

          <!-- Approve -->
          <td>
            <button
              v-if="!company.approved && !company.rejected"
              class="btn btn-success btn-sm"
              @click="approve(company.id)"
            >
              Approve
            </button>

            <button
              v-else-if="company.approved"
              class="btn btn-secondary btn-sm"
              disabled
            >
              Approved
            </button>

            <button
              v-else
              class="btn btn-secondary btn-sm"
              disabled
            >
              Pending
            </button>
          </td>

          <!-- Reject -->
          <td>
            <button
              v-if="!company.rejected && !company.approved"
              class="btn btn-warning btn-sm"
              @click="rejectCompany(company.id)"
            >
              Reject
            </button>

            <button
              v-else-if="company.rejected"
              class="btn btn-secondary btn-sm"
              disabled
            >
              Rejected
            </button>

            <button
              v-else
              class="btn btn-secondary btn-sm"
              disabled
            >
              N/A
            </button>
          </td>

          <!-- Blacklist -->
          <td>
            <button
              v-if="!company.blacklisted"
              class="btn btn-danger btn-sm"
              @click="blacklist(company.id)"
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
      companies: [],
      search: ""
    };
  },

  computed: {
    filteredCompanies() {
      return this.companies.filter(company =>
        company.companyname
          .toLowerCase()
          .includes(this.search.toLowerCase())
      );
    }
  },

  mounted() {
    this.loadCompanies();
  },

  methods: {
    async loadCompanies() {
      const response = await fetch(`${this.$apiBase}/admin/companies`, {
        credentials: "include"
      });

      const data = await response.json();
      this.companies = data.companies;
    },

    async approve(id) {
      await fetch(`${this.$apiBase}/admin/company/${id}/approve`, {
        method: "POST",
        credentials: "include"
      });

      this.loadCompanies();
    },

    async rejectCompany(id) {
      await fetch(`${this.$apiBase}/admin/company/${id}/reject`, {
        method: "POST",
        credentials: "include"
      });

      this.loadCompanies();
    },

    async blacklist(id) {
      await fetch(`${this.$apiBase}/admin/company/${id}/blacklist`, {
        method: "POST",
        credentials: "include"
      });

      this.loadCompanies();
    }
  }
};
</script>