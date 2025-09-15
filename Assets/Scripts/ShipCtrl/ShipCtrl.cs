using System.Collections.Generic;
using UnityEngine;


public enum BrachistochronePhase
{
    None,
    InitialRotation,
    Acceleration,
    Flip,
    Deceleration,
    FinalStop
}
/*
* This script should hold the different control funcitons that any ship will need to navigate to a given waypoint.
* It should also prepare for the case that a ship receive a sequence of waypoints.
*/
public class ShipCtrl : MonoBehaviour
{
    public float maxAcceleration = 50f;
    public float standardAcceleration = 1f;
    private float acceleration = 0f; //The currently set acceleration value
    public float rotationSpeed = 30f;
    private BrachistochronePhase phase = 0;
    private List<GameObject> sequence = new List<GameObject>(); // The sequence of waypoints
    Rigidbody2D rb;
    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        acceleration = 1f;
    }

    // Update is called once per frame
    void Update()
    {

    }

    void FixedUpdate()
    {
        //acceleration = 1f;
        //AdjustVelocity(10f);
        //Vector2 direction = new Vector2(-1, 1);
        //RotateToHeading(direction);
        if (sequence.Count > 0)
        {
            MoveToWaypointNew(sequence[0]);
        }
    }

    public void SetAcceleration(float newAcceleration)
    {
        if (newAcceleration > maxAcceleration)
        {
            acceleration = maxAcceleration;
        }
        else
        {
            acceleration = newAcceleration;
        }
        return;
    }

    public void BurnEngine()
    {
        Vector2 forceToAdd = transform.up * acceleration;
        rb.AddForce(forceToAdd);
    }

    public float RotateToHeading(Vector2 targetDirection)
    {
        // Check if there is a target direction.
        if (targetDirection != Vector2.zero)
        {
            
            // Calculate the target rotation based on the direction.
            Quaternion targetRotation = Quaternion.LookRotation(Vector3.forward, targetDirection);

            // Rotate the ship towards the target rotation.
            transform.rotation = Quaternion.RotateTowards(transform.rotation, targetRotation, rotationSpeed * Time.fixedDeltaTime);

            float angleToTarget = Vector2.SignedAngle(transform.up, targetDirection);
            float remainingTime = Mathf.Abs(angleToTarget) / rotationSpeed;
            return remainingTime;
        }
        else
        {
            return 0.0f;
        }
    }

    // This sets the magnitude of the velocity value
    // This method assumes that the ship is pointing in the correct direction.
    public float AdjustVelocity(float magnitude)
    {
        Debug.Log("AdjustVelocity!!");
        if (rb.linearVelocity.magnitude < magnitude)
        {
            BurnEngine();
        }

        // Clamp the velocity to prevent overshooting the target magnitude.
        if (rb.linearVelocity.magnitude > magnitude)
        {
            rb.linearVelocity = rb.linearVelocity.normalized * magnitude;
            return 0.0f;
        }

        return (rb.linearVelocity.magnitude - magnitude) / acceleration;

    }


    public void MoveToWaypoint(GameObject waypoint)
    {
        Vector2 directionToDestination = waypoint.transform.position - transform.position;
        float distanceToDestination = directionToDestination.magnitude;

        float currentVelocity = rb.linearVelocity.magnitude;

        // Distance needed to come to a full stop at current velocity (assuming we are pointing in the right direction)
        float brakingDistance = (currentVelocity * currentVelocity) / (2 * acceleration);

        // Account for the Flip-Maneuver
        // How for to flip
        // How long will this take?
        // How far will we travel during that flip?
        float angleToFlip = Vector2.Angle(transform.up, -directionToDestination);
        float timeToRotate = angleToFlip / rotationSpeed;
        float coastingDistance = currentVelocity * timeToRotate;

        float totalStoppingDistance = brakingDistance + coastingDistance;

        bool isBraking = distanceToDestination <= totalStoppingDistance;

        Vector2 destinationHeading = isBraking ? -directionToDestination : directionToDestination;
        RotateToHeading(destinationHeading);

        // --- Apply Thrust based on Alignment ---
        float alignment = Vector2.Dot(transform.up, destinationHeading.normalized);

        Debug.Log("Alignment: " + alignment);

        if (alignment > 0.95f)
        {
            BurnEngine();
        }

        // --- Final Stop ---
        if (distanceToDestination < 0.1f && currentVelocity < 0.5f)
        {
            rb.linearVelocity = Vector2.zero;
            sequence.RemoveAt(0);
        }


    }


    public void MoveToWaypointNew(GameObject waypoint)
    {
        Vector2 directionToDestination = waypoint.transform.position - transform.position;
        float distanceToDestination = directionToDestination.magnitude;
        float currentVelocity = rb.linearVelocity.magnitude;

        // Distance needed to come to a full stop at current velocity (assuming we are pointing in the right direction)
        float brakingDistance = (currentVelocity * currentVelocity) / (2 * acceleration);
        float flipBuffer = 1f; // Time cushion to allow is to align more precisely

        float angleToFlip = Vector2.Angle(transform.up, -directionToDestination);
        float timeToRotate = angleToFlip / rotationSpeed;
        float coastingDistance = currentVelocity * timeToRotate + currentVelocity * flipBuffer;

        float totalStoppingDistance = brakingDistance + coastingDistance;

        Vector2 desiredDirection = transform.up; // We are assuming we are pointing in the right direction.
        float alignment = 0f;
        

        switch (phase)
        {
            case BrachistochronePhase.None:
                return;
            case BrachistochronePhase.InitialRotation:
                Vector2 lateralVelocity = rb.linearVelocity - Vector2.Dot(rb.linearVelocity, directionToDestination.normalized) * directionToDestination.normalized;
                desiredDirection = directionToDestination.normalized - lateralVelocity * 0.1f; // The 0.1f is a correction factor to tune.
                alignment = Vector2.Dot(transform.up, desiredDirection.normalized);
                if (alignment > 0.98f)
                {
                    phase = BrachistochronePhase.Acceleration;
                }
                break;
            case BrachistochronePhase.Acceleration:
                lateralVelocity = rb.linearVelocity - Vector2.Dot(rb.linearVelocity, directionToDestination.normalized) * directionToDestination.normalized;
                desiredDirection = directionToDestination.normalized - lateralVelocity * 0.1f; // The 0.1f is a correction factor to tune.
                BurnEngine();
                if (distanceToDestination <= totalStoppingDistance)
                {
                    phase = BrachistochronePhase.Flip;
                }
                break;
            case BrachistochronePhase.Flip:
                desiredDirection = -rb.linearVelocity.normalized;
                alignment = Vector2.Dot(transform.up, desiredDirection.normalized);
                if (alignment > 0.98f && distanceToDestination <= brakingDistance)
                {
                    phase = BrachistochronePhase.Deceleration;
                }
                break;
            case BrachistochronePhase.Deceleration:
                desiredDirection = -rb.linearVelocity.normalized;
                BurnEngine();
                if (distanceToDestination < 10f && currentVelocity < 0.5f)
                {
                    phase = BrachistochronePhase.FinalStop;
                }
                break;
            case BrachistochronePhase.FinalStop:
                rb.linearVelocity = Vector2.zero;
                sequence.RemoveAt(0);
                phase = BrachistochronePhase.None;
                break;
        }

        RotateToHeading(desiredDirection);
        
    }

    public void AddWaypoint(GameObject waypoint)
    {
        sequence.Add(waypoint);
        phase = BrachistochronePhase.InitialRotation;
    }

}
