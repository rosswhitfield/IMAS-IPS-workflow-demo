! compile with: gfortran -I${IMAS_PREFIX}/include/gfortran -o imas_cp_eq imas_cp_eq.f90 -L${IMAS_PREFIX}/lib -limas-gfortran
! run with: ./imas_cp_eq $PWD d3d 1 1 13

program imas_cp_eq
  use ids_routines
  implicit none

  character(len=128) :: user, tokamak, buffer
  integer :: shot, run, imas_backend
  integer :: idx, status, i, j
  type (ids_core_profiles) :: cp
  type (ids_equilibrium) :: eq

  call get_command_argument(1, user)
  call get_command_argument(2, tokamak)
  call get_command_argument(3, buffer)
  read(buffer, *) shot
  call get_command_argument(4, buffer)
  read(buffer, *) run
  call get_command_argument(5, buffer)
  read(buffer, *) imas_backend
  write(*,*) "user = ", trim(user)
  write(*,*) "tokamak = ", trim(tokamak)
  write(*,*) "shot = ", shot
  write(*,*) "run = ", run
  write(*,*) "backend = ", imas_backend

  call ual_begin_pulse_action(imas_backend, shot, run, user, tokamak, '3', idx, status)
  if (status.eq.0) then
     call ual_open_pulse(idx, OPEN_PULSE, '', status)
  end if

  if (status.ne.0) then
     stop 1
  end if

  write(*,*) 'Opened pulse file, idx = ', idx

  call ids_get(idx, "core_profiles", cp)
  call ids_get(idx, "equilibrium", eq)

  call ual_close_pulse(idx, CLOSE_PULSE, '', status)
  if (status.eq.0) then
     call ual_end_action(idx, status)
  end if

  if (status.ne.0) then
     stop 1
  end if

  write(*,*) "Core profiles:"
  write(*,*) "IDS_Properties homogeneous : ", cp%ids_properties%homogeneous_time
  write(*,*) "Size of cp%profiles_1d : ", size(cp%profiles_1d)
  write(*,*) "cp%profiles_1d%time : ",cp%profiles_1d(:)%time
  write(*,*) "Main IDS time : ", cp%time

  do i=1,size(cp%profiles_1d)
     write(*,*) "Time slice i = ", cp%profiles_1d(i)%time
     write(*,*) "rho = ", cp%profiles_1d(i)%grid%rho_tor_norm
     write(*,*) "Electron temperature = ", cp%profiles_1d(i)%electrons%temperature
     write(*,*) "Size of cp%profiles_1d%ion", size(cp%profiles_1d(i)%ion)
     do j=1,size(cp%profiles_1d(i)%ion)
        write(*,*) "Ion(",i,") temperature", cp%profiles_1d(i)%ion(j)%temperature
     end do
  enddo

  write(*,*) "Equilibrium:"
  write(*,*) "IDS_Properties homogeneous : ", eq%ids_properties%homogeneous_time
  write(*,*) "Size of  eq%time_slice: ", size(eq%time_slice)
  write(*,*) "eq%time_slice%time : ", eq%time_slice%time
  write(*,*) "Main IDS time : ", eq%time

  do i=1,size(eq%time_slice)
     write(*,*) "Time slice i = ", eq%time_slice(i)%time
     write(*,*) "rho = ", eq%time_slice(i)%profiles_1d%rho_tor_norm
     write(*,*) "q = ", eq%time_slice(i)%profiles_1d%q
     write(*,*) "b_field_average = ", eq%time_slice(i)%profiles_1d%b_field_average
  enddo

end program imas_cp_eq
