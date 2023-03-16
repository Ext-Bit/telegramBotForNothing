const { createApp } = Vue

createApp({
    data() {
        return {
            data_from_db: {},
            show_input: 0
        }
    },
    methods: {
        reload_table(event) {
            axios.post('/admin-page')
                .then(res => {
                    this.data_from_db = res.data
                })
                .catch(err => {
                    console.log(err)
            })
        },
        change_show_input(id, state) {
            if (this.show_input) {
                console.log(id, Number(state))
                axios.post('/admin-page', {user_id: id, new_state: Number(state)})
                    .then(res => {
                        this.data_from_db = res.data
                    })
                    .catch(err => {
                        console.log(err)
                
                    })
                this.show_input = 0
            }
            else {
                this.show_input = 1
            }
        }
    },
    mounted() {
        axios.post('/admin-page')
            .then(res => {
                this.data_from_db = res.data
            })
            .catch(err => {
                console.log(err)
        })
    }
}).mount('#app')
