package com.example.carrot_backend.user.infrastructure;


import com.example.carrot_backend.user.domain.UserEntity;
import com.example.carrot_backend.user.domain.UserWriter;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

@Repository
@RequiredArgsConstructor
public class UserWriterImpl implements UserWriter{

    private final UserRepository userRepository;

    @Override
    public UserEntity save(UserEntity user) {
        return userRepository.save(user);
    }
}
