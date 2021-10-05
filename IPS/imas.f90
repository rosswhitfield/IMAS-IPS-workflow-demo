program imas
  use ids_routines
  implicit none

  character(len=128) :: user, tokamak, buffer
  integer :: shot, run, imas_backend
  integer :: idx, status, i
  real(ids_real) :: timestamp
  type (ids_core_profiles) :: cp

  write(*,*) "Fortran IMAS program started"
  call get_command_argument(1, user)
  call get_command_argument(2, tokamak)
  call get_command_argument(3, buffer)
  read(buffer, *) shot
  call get_command_argument(4, buffer)
  read(buffer, *) run
  call get_command_argument(5, buffer)
  read(buffer, *) imas_backend
  call get_command_argument(6, buffer)
  read(buffer, *) timestamp
  write(*,*) "user = ", trim(user)
  write(*,*) "tokamak = ", trim(tokamak)
  write(*,*) "shot = ", shot
  write(*,*) "run = ", run
  write(*,*) "backend = ", imas_backend
  write(*,*) "timestamp = ", timestamp

  call ual_begin_pulse_action(imas_backend, shot, run, user, tokamak, '3', idx)
  call ual_open_pulse(idx, OPEN_PULSE, '', status)
  write(*,*) 'Opened pulse file, idx = ', idx

  call ids_get_slice(idx, "core_profiles", cp, timestamp, CLOSEST_INTERP)

  cp%time = timestamp
  cp%global_quantities%ip = cp%global_quantities%ip + timestamp
  cp%profiles_1d(1)%time = timestamp
  cp%profiles_1d(1)%grid%rho_tor_norm = cp%profiles_1d(1)%grid%rho_tor_norm + timestamp

  call ids_put_slice(idx, "core_profiles", cp)

  call ual_close_pulse(idx, OPEN_PULSE, '', status)
  write(*,*) "Program completed"
end program imas
