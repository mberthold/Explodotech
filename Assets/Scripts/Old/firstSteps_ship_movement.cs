/*
using System.Runtime.CompilerServices;
using UnityEngine;
using UnityEngine.InputSystem;

public class ship_movement : MonoBehaviour
{
    public Rigidbody2D shipBody;
    public Vector2 velocity;
    private float vel_x = 0.0f;
    private float vel_y = 0.0f;
    private float acceleration = 0.10f;
    [SerializeField] private fieldOFView fov;
    private float angularSpeed = 0.0f;
    private float angularAcceleration = 0.1f;


    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        velocity = new Vector2(1.0f, 0.0f);
        gameObject.name = "El Presidente";
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 fovOrigin = transform.position;
        fovOrigin[2] = 0;
        fov.SetOrigin(fovOrigin);
        fov.SetDirection(shipBody.rotation);

        var keyboard = Keyboard.current;

        if (keyboard.upArrowKey.IsPressed() == true)
        {
            vel_y += acceleration;
        }

        if (keyboard.downArrowKey.IsPressed() == true)
        {
            vel_y -= acceleration;
        }

        if (keyboard.rightArrowKey.IsPressed() == true)
        {
            vel_x += acceleration;
        }

        if (keyboard.leftArrowKey.IsPressed() == true)
        {
            vel_x -= acceleration;
        }

        if (keyboard.qKey.IsPressed() == true)
        {
            angularSpeed += angularAcceleration;
        }

        if (keyboard.eKey.IsPressed() == true)
        {
            angularSpeed -= angularAcceleration;
        }

        velocity = new Vector2(vel_x, vel_y);
        shipBody.MoveRotation(shipBody.rotation + angularSpeed);
        shipBody.linearVelocity = velocity;


    }
    
}
*/