const admin = {
    template:`
    <div>
    <div class="container">
    <h4 class="text-dark">Welcome!</h4>
        <div class="row">
            <div class="col-md-6">
                <div class="card ">
                    <router-link to="/theater">
                        <div class="card bg-dark border border-dark border-4 rounded-3">
                            <img src="https://wallpaperaccess.com/full/825971.png" alt="THEATERS" style="height:400px">
                            <div class="card-body text-white">
                                <h5 class="card-title">Theaters (and Shows)</h5>
                                <p class="card-text">Theater Management (and Show Management) view to add theaters (shows) or update theater (show) properties.</p>
                                <!-- <a href="#" class="btn btn-primary">Go somewhere</a> -->
                            </div>
                        </div>
                    </router-link>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <router-link to="/movies">
                        <div class="card bg-dark border border-dark border-4 rounded-3">
                            <img src="https://wallpaperaccess.com/full/5511868.jpg" alt="MOVIES" style="height:400px">
                            <div class="card-body text-white">
                                <h5 class="card-title">Movies</h5>
                                <p class="card-text">Movie Management view to add new movies or update movie properties.</p>
                                <!-- <a href="#" class="btn btn-primary">Go somewhere</a> -->
                            </div>
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</div>
    `,
}

export default admin