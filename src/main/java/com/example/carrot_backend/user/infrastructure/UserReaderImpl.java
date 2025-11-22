package com.example.carrot_backend.user.infrastructure;

import com.example.carrot_backend.user.domain.UserEntity;
import com.example.carrot_backend.user.domain.UserReader;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
@RequiredArgsConstructor
public class UserReaderImpl implements UserReader{

    private final UserRepository userRepository;

    @Override
    public Optional<UserEntity> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    @Override
    public boolean existsByEmail(String email) {
        return userRepository.existsByEmail(email);
    }
}
