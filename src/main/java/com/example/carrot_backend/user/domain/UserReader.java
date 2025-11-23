package com.example.carrot_backend.user.domain;

import java.util.Optional;

public interface UserReader {

    Optional<UserEntity> findByEmail(String email);

    boolean existsByEmail(String email);


}
