using UnityEngine;

public class Emitter : MonoBehaviour
{
    public float signalStrength = 1.0f;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }

    public float GetSignalStrength()
    {
        return this.signalStrength;
    }
}
