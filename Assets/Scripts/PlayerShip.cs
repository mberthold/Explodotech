using System.Numerics;
using UnityEngine;
using UnityEngine.InputSystem;
using Vector3 = UnityEngine.Vector3;
using Vector2 = UnityEngine.Vector2;
using Quaternion = UnityEngine.Quaternion;

public class PlayerShip : MonoBehaviour
{

    public GameObject waypointPrefab;


    private Vector3? moveDestination = null;
    private GameObject currentWaypoint;
    private ShipCtrl shipCtrl;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        shipCtrl = GetComponent<ShipCtrl>();
    }

    // Update is called once per frame
    void Update()
    {


    }
   
    public void OnSetWaypoint(InputAction.CallbackContext context)
    {
        Debug.Log("Right-Click");
        if (context.performed)
        {
            // Get the mouse position
            Vector2 mousePosition = Mouse.current.position.ReadValue();
            // Turn that position into the 3D position where we want to place the waypoint.
            Vector3 worldPosition = Camera.main.ScreenToWorldPoint(new Vector3(mousePosition.x, mousePosition.y, 1));

            moveDestination = worldPosition;

            // If a waypoint already exists we should delete it.
            if (currentWaypoint != null)
            {
                Destroy(currentWaypoint);
            }

            // Create the new waypoint
            currentWaypoint = Instantiate(waypointPrefab, worldPosition, Quaternion.identity);
            shipCtrl.AddWaypoint(currentWaypoint);

        }
    }
}
