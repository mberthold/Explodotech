using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerShip : MonoBehaviour
{

    public float moveSpeed = 5f;
    public float rotationSpeed = 100f;

    private Vector2 moveInput;
    private float rotationInput;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        
        // Apply movement
        Vector3 moveDirection = new Vector3(moveInput.x, moveInput.y, 0f);
        transform.position += moveDirection * moveSpeed * Time.deltaTime;

        // Apply rotation
        transform.Rotate(0, 0, -rotationInput * rotationSpeed * Time.deltaTime);
        
    }

    // This method is automatically called when the "Move" action is performed.
    public void OnMove(InputAction.CallbackContext context)
    {
        Debug.Log("OnMove!");
        moveInput = context.ReadValue<Vector2>();
    }

    // This method is automatically called when the "Rotate" action is performed.
    public void OnRotate(InputAction.CallbackContext context)
    {
        Debug.Log("OnRotate!");
        rotationInput = context.ReadValue<float>();
    }
}
