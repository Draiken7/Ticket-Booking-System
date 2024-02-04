const bookings = {
    template:`
    <div>
    <div class="container">
    <div class="mx-left">
        <router-link to='/user'>
            <button class="btn btn-outline-info" title="back">
                <i class="bi bi-skip-backward fs-1"></i>
            </button>
        </router-link>
    </div>
    <div v-if="this.data!=null">
        <div class="container my-2">
            <div>
                <h3>You bookings!</h3>
            </div>
            <div>
                <table class="table table-striped">
                    <tr>
                        <th>S.No.</th>
                        <th>Date of Booking</th>
                        <th>Movie</th>
                        <th>Theater</th>
                        <th>Location</th>
                        <th>Date of Show</th>
                        <th>Time of Show</th>
                        <th>Number of Seats Booked</th>
                        <th>Total Amount Paid</th>
                    </tr>
                    <tr v-for="(booking, index) in this.data">
                        <td>{{index+1}}</td>
                        <td>{{booking.bookingdate}}</td>
                        <td>{{booking.movie}}</td>
                        <td>{{booking.theater}}</td>
                        <td>{{booking.location}}</td>
                        <td>{{booking.showdate}}</td>
                        <td>{{booking.showtime}}</td>
                        <td>{{booking.seats}}</td>
                        <td>{{booking.total}}</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div v-else>
        <h3>No Bookings made yet!</h3>
    </div>
</div>
    </div>
    `,
    data(){
        return{
            data:null,
        }
    },
    async beforeCreate(){
        const res = await fetch('http://127.0.0.1:5000/booking',{
            method:'GET',
            headers:{
                'Authorization':`Bearer ${localStorage.getItem('auth-token')}`
            }
        })
        this.data = await res.json()
    }
}

export default bookings