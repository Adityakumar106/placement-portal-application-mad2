<template>
  <div>

    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>My Drives</h3>
      <div>
        <button class="btn btn-outline-secondary btn-sm me-2" @click="loadDrives">
          Refresh
        </button>
        <button class="btn btn-primary btn-sm" @click="createNewDrive">
          Create Drive
        </button>
      </div>
    </div>

      
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>ID</th>
          <th>Drive Name</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="drive in drives"
          :key="drive.id"
        >

          <td>{{ drive.id }}</td>

          <td>{{ drive.title }}</td>

          <td>
            <span
              v-if="drive.status=='open'"
              class="badge bg-success"
            >
              Open
            </span>

            <span
              v-else
              class="badge bg-secondary"
            >
              Closed
            </span>
          </td>

          <td>

            <!-- Open Drive -->
            <template v-if="drive.status=='open'">

              <button
                class="btn btn-info btn-sm me-2"
                @click="viewDrive(drive.id)"
              >
                View Details
              </button>

              <button
                class="btn btn-danger btn-sm"
                @click="completeDrive(drive.id)"
              >
                Mark as Complete
              </button>

            </template>

            <!-- Closed Drive -->
            <template v-else>

              <div class="dropdown">

                <button
                  class="btn btn-warning btn-sm dropdown-toggle"
                  data-bs-toggle="dropdown"
                >
                  Update
                </button>

                <ul class="dropdown-menu">

                  <li>
                    <a
                      class="dropdown-item"
                      href="#"
                      @click.prevent="restartDrive(drive.id)"
                    >
                      Restart Drive
                    </a>
                  </li>

                  <li>
                    <a
                      class="dropdown-item"
                      href="#"
                      @click.prevent="viewDrive(drive.id)"
                    >
                      View Details
                    </a>
                  </li>

                </ul>

              </div>

            </template>

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
      drives: []
    }
  },

  mounted() {
    this.loadDrives()
  },

  methods: {

    async loadDrives() {
      try {
        const res = await fetch(`${this.$apiBase}/company/drives`, { credentials: "include" })

        if (!res.ok) {
          const err = await res.json().catch(() => ({ message: 'Failed to load drives' }))
          console.error('loadDrives error', err)
          alert(err.message || 'Failed to load drives')
          this.drives = []
          return
        }

        const data = await res.json()
        this.drives = data.drives || []
      } catch (e) {
        console.error(e)
        alert('Network error while loading drives')
        this.drives = []
      }
    },

    createNewDrive() {
      this.$router.push('/company/create-drive')
    },

    viewDrive(id) {
      this.$router.push(`/company/drive/${id}`)
    },

    async completeDrive(id) {

      try {
        const res = await fetch(`${this.$apiBase}/company/drive/${id}/complete`, {
          method: "POST",
          credentials: "include"
        })

        if (!res.ok) {
          const err = await res.json().catch(() => ({ message: 'Failed to complete drive' }))
          console.error('completeDrive error', err)
          alert(err.message || 'Failed to complete drive')
          return
        }

        this.loadDrives()
      } catch (e) {
        console.error(e)
        alert('Network error while completing drive')
      }
    },

    async restartDrive(id) {

      try {
        const res = await fetch(`${this.$apiBase}/company/drive/${id}/restart`, {
          method: "POST",
          credentials: "include"
        })

        if (!res.ok) {
          const err = await res.json().catch(() => ({ message: 'Failed to restart drive' }))
          console.error('restartDrive error', err)
          alert(err.message || 'Failed to restart drive')
          return
        }

        this.loadDrives()
      } catch (e) {
        console.error(e)
        alert('Network error while restarting drive')
      }
    }

  }

}
</script>